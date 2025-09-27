import _ from 'lodash'
import sqlite from '../sqlite/index.js'
import { Post } from '../entities/post.js'

export class PostService {

  protected repo = sqlite.getRepository(Post)

  async save(post: Post): Promise<Post> {
    return this.repo.save(post)
  }

  async query(): Promise<Post[]> {
    return this.repo.find({where: { visited: false}})
  }

  async visited(post: Post) {
    post.visited = true
    await this.repo.save(post)
  }

}
