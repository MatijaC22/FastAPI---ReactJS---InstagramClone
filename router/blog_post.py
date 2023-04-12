from typing import Optional, List, Dict
from fastapi import APIRouter, Query, Path, Body
from pydantic import BaseModel

router = APIRouter(
    prefix = '/blog',
    tags = ['blog']
)

class Image(BaseModel):
    url: str
    alias: str

class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {'key' : 'value'}
    image: Optional[Image] = None

@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        'id': id,
        'data' : blog,
        'version' : version
        }

@router.post('/nex/{id}/comment/{comment_id}')
def create_comment(
    blog: BlogModel, 
    id: int, 
    comment_title: str = Query(
                            None, 
                            title = 'id of the comment',
                            description = 'Some description for comment id',
                            alias = 'commentTitle',
                            deprecated= True
                          ),
    # content: str = Body('Hi how are you')
    content: str = Body(
                        ..., # 3 tockice tako da taj parametar nije optional 
                        min_length = 10,
                        max_length = 20,
                        regex = '^[a-z\s]*$' #da taj string moze biti samo space ili mala slova
                    ),
    # v: Optional[List[str]] = Query(None) #ako zelim vise parametara u query url s istim imenom
    v: Optional[List[str]] = Query(['1.0','1.2','1.4']),
    comment_id : int = Path(gt = 5, le = 10)
  ):
    return {
        'blog' : blog,
        'id' : id,
        'comment_title' : comment_title,
        'content' : content,
        'version' : v,
        'comment_id' : comment_id
    }


def required_functionality():
    return {'message' : 'learning fastAPI is important'}