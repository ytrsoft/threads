import _ from 'lodash'
import { Menu } from '../entities/menu.js'
import { Page } from '../entities/page.js'
import { Item } from '../entities/item.js'
import { Record } from '../entities/record.js'
import sqlite from '../sqlite/index.js'

const menuRepo = sqlite.getRepository(Menu)
const pageRepo = sqlite.getRepository(Page)
const itemRepo = sqlite.getRepository(Item)
const recordRepo = sqlite.getRepository(Record)

export const queryMenus = async (): Promise<Menu[]> => {
  return await menuRepo.find({
    where: {
      visited: false
    }
  })
}

export const saveMenu = async (menu: Menu) => {
  if (menu.id) {
    await menuRepo.save(menu)
  } else {
    const menus: Menu[] = await queryMenus()
    if (!_.isEmpty(menus)) {
      await menuRepo.save(menu)
    }
  }
}

export const queryPages = async (): Promise<Page[]> => {
  return await pageRepo.find({
    where: {
      visited: false
    }
  })
}

export const savePage = async (page: Page) => {
  if (page.id) {
    await pageRepo.save(page)
  } else {
    const pages: Page[] = await queryPages()
    if (!_.isEmpty(pages)) {
      await pageRepo.save(page)
    }
  }
}

export const queryItems = async (): Promise<Item[]> => {
  return await itemRepo.find({
    where: {
      visited: false
    }
  })
}

export const saveItem = async (item: Item) => {
  if (item.id) {
    await itemRepo.save(item)
  } else {
    const items: Item[] = await queryItems()
    if (!_.isEmpty(items)) {
      await itemRepo.save(item)
    }
  }
}

export const queryRecords = async (): Promise<Record[]> => {
  return await recordRepo.find({
    where: {
      visited: false
    }
  })
}

export const saveRecord = async (record: Record) => {
  if (record.id) {
    await recordRepo.save(record)
  } else {
    const records: Record[] = await queryRecords()
    if (!_.isEmpty(records)) {
      await recordRepo.save(record)
    }
  }
}

