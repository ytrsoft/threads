import { Entity, Column } from 'typeorm'
import Base from './base.js'

@Entity()
export class Detail extends Base {

  @Column({ type: 'varchar', length: 255, nullable: true })
  fid!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  tid!: string

  @Column({ type: 'varchar', length: 255 })
  name!: string

  @Column('text', { nullable: true })
  desc!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  region!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  age!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  beauty!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  price!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  service!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  wechat!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  qq!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  phone!: string

  @Column({ type: 'varchar', length: 255, nullable: true })
  imgs!: string
}
