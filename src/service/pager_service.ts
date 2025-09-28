import _ from 'lodash'
import { Pager } from '../entities/pager.js'
import { BaseService, Entity, SingleEntity } from './base_service.js'

export class PagerService extends BaseService<Pager> {

  constructor() {
    super(Pager)
  }

  public async gen(pager: SingleEntity<Pager>) {
    const maxpage = pager?.pages || 0
    const entities: Entity<Pager> = []
    for (let i = 1; i <= maxpage; i++) {
      entities.push({
        page: i,
        cid: pager.cid,
        pages: maxpage
      })
    }
    await super.save(entities)
  }

}
