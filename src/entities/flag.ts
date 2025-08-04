import { Entity, Column } from 'typeorm'
import Base from './base.js'

@Entity()
export class Flag extends Base {
  @Column({ type: 'varchar', length: 255, nullable: true })
  fid!: string

  @Column({ type: 'int', nullable: true })
  page!: number

  @Column({ type: 'int', nullable: true })
  pages!: number
}
