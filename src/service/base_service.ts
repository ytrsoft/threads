import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'
import BaseEntity from '../entities/base.js'
import sqlite from '../sqlite/index.js'
import { Repository, EntityTarget, DeepPartial, FindManyOptions } from 'typeorm'

export type Entity<T> = DeepPartial<T> | Array<DeepPartial<T>>
export type ArrayEntity<T> = Array<DeepPartial<T>>

export abstract class BaseService<T extends BaseEntity> {

  protected repo: Repository<T>

  constructor(entity: EntityTarget<T>) {
    this.repo = sqlite.getRepository(entity)
  }

  public async save(entities: Entity<T>): Promise<Entity<T>> {
    if (!_.isArray(entities)) {
      entities = [entities]
    }
    if (_.isEmpty(entities)) {
      return []
    }
    entities = entities.map((entity) => {
      if (!entity?.id) {
        entity.id = uuidv4().replace(/-/g, '')
      }
      return entity
    })
    const targets: Entity<T> = []
    for (let i = 0; i < entities.length; i++) {
      const where: FindManyOptions<T> = {
        where: {
          id: entities[i].id as any
        }
      }
      const exists = await this.repo.exists(where)
      if (!exists) {
        targets.push(entities[i])
      }
    }
    return await this.repo.save(targets)
  }

  public async visited(t: T) {
    t.visited = true
    return await this.repo.save(t)
  }

  public async queries(): Promise<ArrayEntity<T>> {
    const where: FindManyOptions<T> = {
      where: {
        visited: false as any
      }
    }
    return this.repo.find(where)
  }
}
