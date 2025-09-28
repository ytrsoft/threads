import { Entity, Column } from 'typeorm'
import BaseEntity from './base.js'

/**
 * 标记表
 */
@Entity('marker')
export class Marker extends BaseEntity {
  // 菜单id
  @Column({ type: 'varchar', length: 255, nullable: true })
  cid!: string

  // 帖子id
  @Column({ type: 'varchar', length: 255, nullable: true })
  pid!: string
}

export type TMaker = Partial<Maker>
