import _ from 'lodash'
import { Pager } from '../entities/pager.js'
import { BaseService, Entity } from './base_service.js'

export class PagerService extends BaseService<Pager> {

  constructor() {
    super(Pager)
  }

  public async gen(pager: Pager) {
    const maxpage = pager?.pages || 0
    const entities: Entity<Pager> = []
    for (let i = 1; i <= maxpage; i++) {
      pager.page = i
      entities.push(pager)
    }
    await super.save(entities)
  }

}
