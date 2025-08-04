import { log } from 'crawlee'
import { DataSource } from 'typeorm'
import { Menu } from '../entities/menu.js'
import { Flag } from '../entities/flag.js'
import { Item } from '../entities/item.js'
import { Detail } from '../entities/detail.js'

const sqlite: DataSource = new DataSource({
  type: 'sqlite',
  synchronize: true,
  database: 'src/sqlite/dataset.sqlite',
  entities: [
    Menu,
    Flag,
    Item,
    Detail
  ]
})

try {
  await sqlite.initialize()
} catch({ message }: any) {
  log.error(String(message))
}

export default sqlite
