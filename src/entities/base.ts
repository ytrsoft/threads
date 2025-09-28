import {
  CreateDateColumn,
  UpdateDateColumn,
  Column,
  BaseEntity as TypeOrmBaseEntity,
  PrimaryColumn,
} from 'typeorm'

/**
 * 公共基类
 */
export default abstract class BaseEntity extends TypeOrmBaseEntity {
  // 主键
  @PrimaryColumn({ type: 'varchar', length: 36 })
  id!: string

  // 创建时间
  @CreateDateColumn({ type: 'datetime' })
  created!: Date

  // 更新时间
  @CreateDateColumn({ type: 'datetime' })
  updated!: Date

  // 标记状态
  @Column({ type: 'boolean', default: false })
  visited!: boolean
}
