from fastapi import Depends, HTTPException, status, APIRouter, Response
from .. import schames, databas, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote",tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote : schames.Vote, db: Session = Depends(databas.get_db), current_user : int =  Depends(oauth2.get_current_user)):

    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id :  {vote.post_id} dose not exites")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has alredy voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id )
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote "}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote dose not exites")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}

