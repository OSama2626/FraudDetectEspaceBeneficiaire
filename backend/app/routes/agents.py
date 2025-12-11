from sqlalchemy.orm import joinedload
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List

from ..core.db import get_db
from ..models.user import User, UserRole
from ..models.bank import Bank
# Import du modèle chèque
from ..models.cheque import Cheque
from ..utils.auth import get_current_user

# --- IMPORT WEBSOCKET ---
from ..services.websocket_manager import manager

router = APIRouter(
    tags=["Agents Management"]
)


@router.put("/confirm-reset")
def confirm_password_reset(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    clerk_id = current_user.get("user_id")
    agent = db.query(User).filter(User.clerk_id == clerk_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé.")
    agent.must_reset_password = False
    db.commit()
    return {"status": "success"}


@router.get("/cheques/me")
def get_my_cheques(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # 1. Récupérer l'ID Clerk
    clerk_id = current_user.get("user_id")

    # 2. Trouver l'agent lié à ce Clerk
    agent = db.query(User).filter(
        User.clerk_id == clerk_id,
        User.role == UserRole.AGENT
    ).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent non trouvé")

    if not agent.bank_id:
        raise HTTPException(
            status_code=400, detail="Aucune banque associée à cet agent.")

    # On sélectionne les chèques :dont le bénéficiaire appartient à la banque/branche de l’agent et qui sont "pending" ou "uploaded"
    beneficiaire_condition = (
        db.query(Cheque, User)
        .join(User, Cheque.beneficiaire_id == User.id)
        .filter(
            User.bank_id == agent.bank_id,
            Cheque.status.in_(["pending", "uploaded"])
            
        )
    )

    # 1. Chèques dont la banque cible = banque de l’agent
    cheques_meme_banque_raw = beneficiaire_condition.filter(
        Cheque.banque_cible_id == agent.bank_id
    ).all()

    cheques_meme_banque = [
        {
            "cheque": {
                **cheque.__dict__,
                "imageUrl": f"/public/{cheque.image_url}"
            },
            "beneficiaire": {
                "id": beneficiaire.id,
                "name": f"{beneficiaire.first_name} {beneficiaire.last_name}",
                "email": beneficiaire.email
            }
        }
        for cheque, beneficiaire in cheques_meme_banque_raw
    ]

    # 2. Chèques dont la banque cible ≠ banque de l’agent
    cheques_autre_banque_raw = beneficiaire_condition.filter(
        Cheque.banque_cible_id != agent.bank_id
    ).all()

    cheques_autre_banque = [
        {
            "cheque": {
                **cheque.__dict__,
                "imageUrl":  f"/public/{cheque.image_url}"
            },
            "beneficiaire": {
                "id": beneficiaire.id,
                "name": f"{beneficiaire.first_name} {beneficiaire.last_name}",
                "email": beneficiaire.email
            }
        }
        for cheque, beneficiaire in cheques_autre_banque_raw
    ]
    # --- RETURN ---
    return {
        "agentName": f"{agent.first_name} {agent.last_name}",
        "agentEmail": agent.email,
        "agentBankId": agent.bank_id,
        "cheques_meme_banque": cheques_meme_banque,
        "cheques_autre_banque": cheques_autre_banque,
    }


@router.post("/cheque/transmettre/{cheque_id}")
async def transmettre_cheque(
    cheque_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    clerk_id = current_user.get("user_id")

    agent = db.query(User).filter(
        User.clerk_id == clerk_id,
        User.role == UserRole.AGENT
    ).first()

    if not agent:
        raise HTTPException(404, "Agent non trouvé.")

    cheque = db.query(Cheque).filter(Cheque.id == cheque_id).first()

    if not cheque:
        raise HTTPException(404, "Chèque introuvable.")

    #if cheque.agent_actuel_id != agent.id:
        #raise HTTPException(403, "Vous n'avez pas accès à ce chèque.")

    if cheque.banque_cible_id == agent.bank_id:
        raise HTTPException(
            400, "Ce chèque doit être traité ici, pas transmis.")

    agent_cible = db.query(User).filter(
        User.bank_id == cheque.banque_cible_id,
        User.role == UserRole.AGENT
    ).first()

    if not agent_cible:
        raise HTTPException(404, "Aucun agent trouvé pour cette banque.")

    # Transmission
    cheque.status = "transmitted"
    cheque.agent_actuel_id = agent_cible.id

    db.commit()

    # --- AJOUT NOTIFICATION WEBSOCKET ---
    try:
        if agent_cible.clerk_id:
            await manager.send_personal_message(
                {
                    "type": "CHEQUE_RECEIVED",
                    "title": "Nouveau chèque reçu",
                    "message": f"Le chèque #{cheque.id} vous a été transmis pour traitement.",
                    "cheque_id": cheque.id
                },
                agent_cible.clerk_id
            )
            print(f"🔔 Notification envoyée à {agent_cible.clerk_id}")
    except Exception as e:
        print(f"⚠️ Erreur notification WS: {e}")
    # ------------------------------------

    return {"message": "Chèque transmis avec succès"}


@router.get("/cheques/transmis")
def get_cheques_transmis(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    clerk_id = current_user.get("user_id")
    agent = db.query(User).filter(
        User.clerk_id == clerk_id,
        User.role == UserRole.AGENT
    ).first()

    cheques = (
        db.query(Cheque)
        .join(User, Cheque.beneficiaire_id == User.id)
        .join(Bank, User.bank_id == Bank.id)
        .options(joinedload(Cheque.beneficiaire))
        .filter(
            Cheque.agent_actuel_id == agent.id,
            Cheque.status == "transmitted"
        )
        .all()
    )

    # Transformer pour renvoyer la structure attendue côté frontend
    result = []
    for ch in cheques:
        result.append({
            "cheque": {
                "id": ch.id,
                "imageUrl": f"/public/{ch.image_url}",
                "status": ch.status
            },
            "beneficiaire": {
                "id": ch.beneficiaire.id,
                "name": f"{ch.beneficiaire.first_name} {ch.beneficiaire.last_name}",
                "bankName": ch.beneficiaire.bank.name


            }
        })
    return result


@router.get("/me")
def get_my_agent(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    clerk_id = current_user.get("user_id")

    if clerk_id is None:
        raise HTTPException(
            status_code=401, detail="Utilisateur non authentifié")

    agent = db.query(User).filter(
        User.clerk_id == clerk_id,
        User.role == UserRole.AGENT
    ).first()

    if agent is None:
        raise HTTPException(status_code=404, detail="Agent introuvable")

    return {
        "id": agent.id,
        "name": f"{agent.last_name} {agent.first_name}",
        "email": agent.email,
        "bankId": agent.bank_id,
    }


@router.get("/cheques/traites")
def get_cheques_traite(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    clerk_id = current_user.get("user_id")
    agent = db.query(User).filter(User.clerk_id == clerk_id,
                                  User.role == UserRole.AGENT).first()

    cheques = (
        db.query(Cheque)
        .join(User, Cheque.beneficiaire_id == User.id)
        .options(joinedload(Cheque.beneficiaire))
        .filter(Cheque.agent_actuel_id == agent.id, Cheque.status.in_(["rejected", "approved"]))
        .all()
    )

    result = []
    for ch in cheques:
        result.append({
            "cheque": {
                "id": ch.id,
                "date_depot": ch.date_depot,
                "imageUrl": f"/public/{ch.image_url}",
                "status": ch.status
            },
            "beneficiaire": {
                "id": ch.beneficiaire.id,
                "name": f"{ch.beneficiaire.first_name} {ch.beneficiaire.last_name}",
                "bankName": ch.beneficiaire.bank.name if ch.beneficiaire.bank else ""
            }
        })

    return result