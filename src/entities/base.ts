import {
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
  Column,
  BaseEntity as TypeOrmBaseEntity
} from 'typeorm'

export default abstract class BaseEntity extends TypeOrmBaseEntity {
  @PrimaryGeneratedColumn('uuid')
  id?: string

  @CreateDateColumn({ type: 'datetime' })
  created?: Date

  @UpdateDateColumn({ type: 'datetime' })
  updated?: Date

  @Column({ default: false })
  visited?: boolean
}
