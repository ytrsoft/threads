import { Entity, Column } from 'typeorm'
import Base from './base.js'

@Entity()
export class Menu extends Base {
  @Column()
  fid?: string

  @Column()
  label?: string
}
