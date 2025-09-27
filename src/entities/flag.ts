import { Entity, Column } from 'typeorm'
import BaseEntity from './base.js'

/**
 * 详情标记表
 */
@Entity('flag')
export class Flag extends BaseEntity {
  // 菜单id
  @Column({ type: 'varchar', length: 255, nullable: true })
  cid?: string

  // 帖子id
  @Column({ type: 'varchar', length: 255, nullable: true })
  pid?: string
}
