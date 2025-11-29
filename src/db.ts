import { DataSource } from 'typeorm'
import { Menu, Post, Image } from './entities/index.js'

export const AppDataSource = new DataSource({
  type: 'sqlite',
  database: 'dataset.sqlite',
  synchronize: true,
  logging: false,
  entities: [Menu, Post, Image],
  enableWAL: true
})

export const initDB = async () => {
  if (!AppDataSource.isInitialized) {
    await AppDataSource.initialize()
  }
}
