import _ from 'lodash'
import { Post } from '../entities/post.js'
import { BaseService } from './base_service.js'

export class PostService extends BaseService<Post> {

  constructor() {
    super(Post)
  }

}
