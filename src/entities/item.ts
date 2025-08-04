import { Entity, Column } from 'typeorm'
import Base from './base.js'

@Entity()
export class Item extends Base {
  @Column({ type: 'varchar', length: 255, nullable: true })
  fid!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  tid!: string
}
