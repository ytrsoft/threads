import { log } from 'crawlee'
import { DataSource } from 'typeorm'
import { Category } from '../entities/category.js'
import { Pager } from '../entities/pager.js'
import { Marker } from '../entities/marker.js'
import { Post } from '../entities/post.js'
import { Image } from '../entities/image.js'

const sqlite: DataSource = new DataSource({
  type: 'sqlite',
  synchronize: true,
  database: 'src/sqlite/dataset.sqlite',
  entities: [
    Category,
    Pager,
    Marker,
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
