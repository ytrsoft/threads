import { Entity, Column, PrimaryColumn, Index } from 'typeorm'
import BaseEntity from './BaseEntity.js'

@Entity()
export class Post extends BaseEntity {
  @PrimaryColumn({ type: 'varchar', length: 36 })
  id!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  title!: string

  @Column({ type: 'text', nullable: true })
  description!: string

  @Column({ type: 'varchar', length: 36, nullable: true })
  region!: string

  @Column({ type: 'varchar', nullable: true })
  age!: string

  @Column({ type: 'varchar', nullable: true })
  score!: string

  @Column({ type: 'varchar', nullable: true })
  price!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  service!: string

  @Column({ type: 'varchar', length: 50, nullable: true })
  wechat!: string

  @Column({ type: 'varchar', length: 50, nullable: true })
  qq!: string

  @Column({ type: 'varchar', length: 50, nullable: true })
  phone!: string

  @Column({ type: 'varchar', length: 36, nullable: true })
  @Index()
  mid!: string
}
