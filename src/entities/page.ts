import { Entity, Column } from 'typeorm'
import Base from './base.js'

@Entity()
export class Pages extends Base {
  @Column({ type: 'varchar', length: 255, nullable: true })
  fid?: string

  @Column({ type: 'int', nullable: true })
  current?: number

  @Column({ type: 'int', nullable: true })
  max?: number
}
