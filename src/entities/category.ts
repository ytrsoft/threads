import { Entity, Column } from 'typeorm'
import BaseEntity from './base.js'

/**
 * 菜单表
 */
@Entity('category')
export class Category extends BaseEntity {
  // 菜单名称
  @Column({ type: 'varchar', length: 36, nullable: true })
  title!: string
}

export type TCategory = Partial<Category>
