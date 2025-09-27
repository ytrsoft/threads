import { log } from 'crawlee'
import { DataSource } from 'typeorm'
import { Category } from '../entities/category.js'
import { Page } from '../entities/page.js'
import { Flag } from '../entities/flag.js'
import { Post } from '../entities/post.js'
import { Image } from '../entities/image.js'

const sqlite: DataSource = new DataSource({
  type: 'sqlite',
  synchronize: true,
  database: 'src/sqlite/dataset.sqlite',
  entities: [
    Category,
    Page,
    Flag,
    Post,
    Image
  ]
})

try {
  await sqlite.initialize()
} catch({ message }: any) {
  log.error(String(message))
}

export default sqlite
