import { Entity, Column } from 'typeorm'
import BaseEntity from './base.js'

/**
 * 分页标记表
 */
@Entity('pager')
export class Pager extends BaseEntity {

  // 菜单id
  @Column({ type: 'varchar', length: 255, nullable: true })
  cid!: string

  // 页码
  @Column({ type: 'int', nullable: true })
  page!: number

  // 总页数
  @Column({ type: 'int', nullable: true })
  pages!: number
}

export type TPager = Partial<Pager>
