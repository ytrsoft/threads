import { Entity, Column } from 'typeorm'
import BaseEntity from './base.js'

/**
 * 帖子表
 */
@Entity('post')
export class Post extends BaseEntity {
  // 标题
  @Column({ type: 'varchar', length: 255, nullable: true })
  title?: string

  // 描述
  @Column({ type: 'text', nullable: true })
  desc?: string

  // 地区
  @Column({ type: 'varchar', length: 255, nullable: true })
  region?: string

  // 年龄
  @Column({ type: 'varchar', length: 255, nullable: true })
  age?: number

  // 评分
  @Column({ type: 'varchar', length: 255, nullable: true })
  score?: number

  // 价格
  @Column({ type: 'varchar', length: 255, nullable: true })
  price?: number

  // 服务
  @Column({ type: 'varchar', length: 255, nullable: true })
  service?: string

  // 微信号码
  @Column({ type: 'varchar', length: 255, nullable: true })
  wechat?: string

  // QQ号码
  @Column({ type: 'varchar', length: 255, nullable: true })
  qq?: string

  // 电话号码
  @Column({ type: 'varchar', length: 255, nullable: true })
  phone?: string

  // 菜单id
  @Column({ type: 'varchar', length: 255, nullable: true })
  cid?: string
}
