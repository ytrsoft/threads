import { Entity, Column } from 'typeorm'
import Base from './base.js'

@Entity()
export class Menu extends Base {
  @Column({ type: 'varchar', length: 255, nullable: true })
  fid?: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  label?: string
}
