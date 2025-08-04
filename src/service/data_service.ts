import { log } from 'crawlee'
import _ from 'lodash'
import { Menu } from '../entities/menu.js'
import { Item } from '../entities/item.js'
import { Record } from '../entities/record.js'
import sqlite from '../sqlite/index.js'
import { Pages } from '../entities/page.js'

const menuRepo = sqlite.getRepository(Menu)
const PagesRepo = sqlite.getRepository(Pages)
const itemRepo = sqlite.getRepository(Item)
const recordRepo = sqlite.getRepository(Record)

export const queryMenus = async (): Promise<Menu[]> => {
  return await menuRepo.find({
    where: {
      visited: false
    }
  })
}

export const saveMenus = async (menus: Menu[]) => {
  for (let i = 0; i < menus.length; i++) {
    await saveMenu(menus[i])
  }
}

export const saveMenu = async (menu: Menu) => {
  const menus: Menu[] = await menuRepo.find({
    where: {
      fid: menu.fid
    }
  })
  if (_.isEmpty(menus)) {
    await menuRepo.save(menu)
    log.info('[MENU]<CREATE> ' + JSON.stringify(menu))
  }
}

export const queryPages = async (): Promise<Pages[]> => {
  return await PagesRepo.find({
    where: {
      visited: false
    }
  })
}

export const savePages = async (pages: Pages) => {
  const _pages: Pages[] = await PagesRepo.find({
    where: {
      fid: pages.fid
    }
  })
  if (_.isEmpty(_pages)) {
    const maxPages = pages.max as number
    for (let i = 1; i <= maxPages; i++) {
      pages.current = i
      await PagesRepo.save(pages)
      log.info('[PAGES]<CREATE> ' + JSON.stringify(pages))
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
    if (_.isEmpty(items)) {
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
    if (_.isEmpty(records)) {
      await recordRepo.save(record)
    }
  }
}

