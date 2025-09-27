import _ from 'lodash'
import sqlite from '../sqlite/index.js'
import { Category } from '../entities/category.js'

export class CategoryService {

  protected repo = sqlite.getRepository(Category)

  async query(): Promise<Category[]> {
    return this.repo.find({where: {visited: false}})
  }

  async visited(category: Category) {
    category.visited = true
    await this.repo.save(category)
  }

  async save(categories: Partial<Category>[]): Promise<Category[]> {
    if (_.isEmpty(categories)) return []
    return await this.repo.save(categories)
  }

}
