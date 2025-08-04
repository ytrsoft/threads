import { Entity, Column } from 'typeorm'
import Base from './base.js'

@Entity()
export class Item extends Base {
  @Column()
  fid?: string

  @Column()
  tid?: string
}
