import _ from 'lodash'
import { Category } from '../entities/category.js'
import { BaseService } from './base_service.js'

export class CategoryService extends BaseService<Category> {

  constructor() {
    super(Category)
  }

}
