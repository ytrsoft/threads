import { Entity, Column, PrimaryGeneratedColumn, Index } from 'typeorm'
import BaseEntity from './BaseEntity.js'

@Entity()
export class Image extends BaseEntity {
  @PrimaryGeneratedColumn('uuid')
  id!: string

  @Column({ type: 'varchar', length: 500, nullable: true })
  src!: string

  @Column({ type: 'varchar', length: 36 })
  @Index()
  pid!: string
}
