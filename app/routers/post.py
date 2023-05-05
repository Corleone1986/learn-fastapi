from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional , List
from sqlalchemy.orm import Session
from ..databas import engine ,get_db
from .. import models, utils, oauth2
from ..schames import Post,PostBase,PostCreate, Postout
from sqlalchemy import func 



router = APIRouter(
    prefix="/posts",
    tags=['Posts']
    )






@router.get("/", response_model=List[Post])
def user_post(db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user), limit: int = 10, skip : int = 0, search : Optional[str] = ""):
    # curser.execute("""SELECT * FROM posts """)
    # posts = curser.fetchall()
    # print(posts)
    # Get posts from user is Online // logined 
    # posts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()
    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).all()
    return  posts


'''''
@app.post("/create")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title {payload['title']} and content {payload['content']}"}
'''''

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    ''' This is for read from Body
    posts_dict = new_post.dict()
    posts_dict['id'] = randrange(0, 10000000)
    my_posts.append(posts_dict)
    '''
    # curser.execute("""INSERT INTO posts (title , content , published) VALUES (%s, %s , %s) RETURNING * """, (post.title, post.content, post.published))
    # new_posts = curser.fetchone()
    # conn.commit()
    # new_posts = models.Posts(title =post.title,content =  post.content,published = post.published)
    
    new_posts = models.Posts(owner_id =current_user.id , **post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return  new_posts
    
'''
@router.get("/lates")
def get_lates_post():
    post = my_posts[len(my_posts) - 1]
    return {"detail": post}
'''
@router.get("/{id}", response_model=Post)
def get_posts(id: int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # curser.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = find_post(id)
    # post = curser.fetchone()

    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    result = db.query(models.Posts, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.id == id).first()

    
    if not post:
        # , Hard Coding
        # response.status_code = 404 
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"the post with {id} was not founded "}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not founded ")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    return  post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # curser.execute("""DELETE FROM posts WHERE id= %s RETURNING * """, (str(id),))
    # deleted_post = curser.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    deleted_post = db.query(models.Posts).filter(models.Posts.id == id)
    post = deleted_post.first()
    print(current_user.id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not exites")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    # my_posts.pop(index)
    # return {"message": "post was succefuly is deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(id:int, post : PostCreate , db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # curser.execute("""UPDATE  posts SET title = %s , content = %s  , published = %s WHERE id= %s  RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = curser.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    updated_post = db.query(models.Posts).filter(models.Posts.id == id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not exites")
    if updated_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    # post_dict = post.dict()
    # post_dict["id"] = id 
    # my_posts[index] = post_dict
    return updated_post.first()