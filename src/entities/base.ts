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
  @PrimaryColumn()
  id!: string

  // 创建时间
  @CreateDateColumn()
  created!: Date

  // 更新时间
  @UpdateDateColumn()
  updated!: Date

  // 标记状态
  @Column({ default: false })
  visited!: boolean
}
