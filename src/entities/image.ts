import { Column, Entity } from 'typeorm'
import BaseEntity from './base.js'

/**
 * 图片表
 */
@Entity('image')
export class Image extends BaseEntity {
  // 图片路径
  @Column({ type: 'varchar', length: 255, nullable: true })
  src!: string

  // 帖子id
  @Column({ type: 'varchar', length: 255, nullable: true })
  pid!: string
}

export type TImage = Partial<Image>
