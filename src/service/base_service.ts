import _ from 'lodash'
import { v4 as uuidv4 } from 'uuid'
import BaseEntity from '../entities/base.js'
import sqlite from '../sqlite/index.js'
import { Repository, EntityTarget, DeepPartial, FindManyOptions, Like } from 'typeorm'

export type SingleEntity<T> = DeepPartial<T>
export type ArrayEntity<T> = Array<DeepPartial<T>>
export type Entity<T> = SingleEntity<T> | ArrayEntity<T>
export type SortOrder = Uppercase<string> | Lowercase<string>

export interface PageParam {
  pageSize: number
  pageNumber: number
  filters?: Record<string, string>
  sortField?: string
  sortOrder?: SortOrder
}

export interface PageResult<T> {
  data: T
  total: number
  pageNumber: number
  pageSize: number
  totalPages: number
}

/**
 * 服务基类
 */
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

  public async queryForList(): Promise<ArrayEntity<T>> {
    const where: FindManyOptions<T> = {
      where: {
        visited: false as any
      }
    }
    return this.repo.find(where)
  }

  public async pageForList(page: PageParam): Promise<PageResult<ArrayEntity<T>>> {
    const { pageNumber, pageSize, filters, sortField, sortOrder } = page
    let where: any = {}
    if (filters && Object.keys(filters).length > 0) {
      where = Object.keys(filters).map((key) => ({
        [key]: Like(`%${filters[key]}%`)
      }))
    }
    const orderValue = (sortOrder ?? 'ASC').toString().toUpperCase() as 'ASC' | 'DESC'
    const [data, total] = await this.repo.findAndCount({
      where,
      order: sortField ? { [sortField]: orderValue } as any : {},
      skip: (pageNumber - 1) * pageSize,
      take: pageSize,
    })
    return {
      data,
      total,
      pageNumber,
      pageSize,
      totalPages: Math.ceil(total / pageSize),
    }
  }

  public async queryById(id: string): Promise<SingleEntity<T> | null> {
    return await this.repo.findOne({
      where: { id } as any,
    })
  }
}
