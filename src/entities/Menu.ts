import { Entity, Column, PrimaryColumn } from 'typeorm'
import BaseEntity from './BaseEntity.js'

@Entity()
export class Menu extends BaseEntity {
  @PrimaryColumn({ type: 'varchar', length: 36 })
  id!: string

  @Column({ type: 'varchar', length: 100, nullable: true })
  name!: string
}
