import {
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
  Column,
  BaseEntity as TypeOrmBaseEntity
} from 'typeorm'

export default abstract class BaseEntity extends TypeOrmBaseEntity {
  @PrimaryGeneratedColumn('uuid')
  id!: string

  @CreateDateColumn({ type: 'datetime' })
  created!: Date

  @UpdateDateColumn({ type: 'datetime' })
  updated!: Date

  @Column({ type: 'boolean', default: false })
  visited!: boolean
}
