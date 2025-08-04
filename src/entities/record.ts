import { Entity, Column } from 'typeorm'
import Base from './base.js'

@Entity()
export class Record extends Base {
  @Column()
  name?: string

  @Column('text', { nullable: true })
  desc?: string

  @Column({ nullable: true })
  region?: string

  @Column({ nullable: true })
  age?: string

  @Column({ nullable: true })
  beauty?: string

  @Column({ nullable: true })
  price?: string

  @Column({ nullable: true })
  service?: string

  @Column({ nullable: true })
  wechat?: string

  @Column({ nullable: true })
  qq?: string

  @Column({ nullable: true })
  phone?: string
}
