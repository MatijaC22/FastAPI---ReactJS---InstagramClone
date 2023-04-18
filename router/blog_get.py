from router.blog_post import required_functionality
from fastapi import APIRouter, status, Response, Depends
from enum import Enum
from typing import Optional

router = APIRouter(
    prefix = '/blog',
    tags = ['blog']
)


@router.get(
    '/all', 
    summary="Retrieve all blogs", 
    description='This api call simulates fetching all blogs',
    response_description='bla bla bla is reponse description'
)
def get_all_blogs(
    page = 1 , 
    page_size: Optional[int] = None, 
    req_parameter: dict = Depends(required_functionality)
):
    return {
        "message": f'All {page_size} logged on page {page}', 
        'req' : req_parameter 
        }

@router.get('/{id}/comments/{commet_id}', tags = ['comment'])
def get_comment(id: int, comment_id:int, valid: bool = True, username:Optional[str] = None):
    """
    Simulates retieving a comment of a blog
    
    - **id** mandatory path parameter
    - **comment** mandatory path parameter
    - **valid** optional query parameter
    - **username** optional query parameter
    """
    return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}

class BlogType(str, Enum):
    short =  'short'
    story = 'story'
    howto = 'howto'

@router.get('/type/{type}')
def get_type(type:BlogType):
    return {"message": f'blog type {type}'}


@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message":f'blog {id} not found'}
    else: 
        response.status_code = status.HTTP_200_OK
        return {"message":f'blog wiht id {id}'}
