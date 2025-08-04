import { log } from 'crawlee'
import { DataSource } from 'typeorm'
import { Menu } from '../entities/menu.js'
import { Pages } from '../entities/page.js'
import { Item } from '../entities/item.js'
import { Record } from '../entities/record.js'

const sqlite: DataSource = new DataSource({
  type: 'sqlite',
  synchronize: true,
  database: 'src/sqlite/dataset.sqlite',
  entities: [
    Menu,
    Pages,
    Item,
    Record
  ]
})

try {
  await sqlite.initialize()
} catch({ message }: any) {
  log.error(String(message))
}

export default sqlite
