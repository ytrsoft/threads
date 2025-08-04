import { Entity, Column } from 'typeorm'
import Base from './base.js'

@Entity()
export class Page extends Base {
  @Column()
  fid?: string

  @Column('int')
  current?: number

  @Column('int')
  max?: number
}
