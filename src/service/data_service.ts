import { log } from 'crawlee'
import _ from 'lodash'
import { Menu } from '../entities/menu.js'
import { Item } from '../entities/item.js'
import { Detail } from '../entities/detail.js'
import { Flag } from '../entities/flag.js'
import sqlite from '../sqlite/index.js'

const menuRepo = sqlite.getRepository(Menu)
const flagRepo = sqlite.getRepository(Flag)
const itemRepo = sqlite.getRepository(Item)
const detailRepo = sqlite.getRepository(Detail)

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

export const queryFlag = async (): Promise<Flag[]> => {
  return await flagRepo.find({
    where: {
      visited: false
    }
  })
}

export const saveFlag = async (flag: Flag) => {
  const flags: Flag[] = await flagRepo.find({
    where: {
      fid: flag.fid
    }
  })
  if (_.isEmpty(flags)) {
    for (let page = 1; page <= flag.pages; page++) {
      flag.page = page
      await flagRepo.save(flag)
      log.info('[FLAG]<CREATE> ' + JSON.stringify(flag))
    }
  }
}

export const vistedFlag = async (flag: Flag) => {
  flag.visited = true
  await flagRepo.save(flag)
  log.info('[FLAG]<UPDATE> ' + JSON.stringify(flag))
}

export const saveItems = async (items: Item[], flag: Flag) => {
  for (let i = 0; i < items.length; i++) {
    await saveItem(items[i])
  }
  await vistedFlag(flag)
}

export const saveItem = async (item: Item) => {
 const _items: Item[] = await itemRepo.find({
    where: {
      tid: item.tid
    }
  })
  if (_.isEmpty(_items)) {
    await itemRepo.save(item)
    log.info('[ITEM]<CREATE> ' + JSON.stringify(item))
  }
}

export const queryItems = async (): Promise<Item[]> => {
  return await itemRepo.find({
    where: {
      visited: false
    }
  })
}

export const vistedItem = async (item: Item) => {
  item.visited = true
  await itemRepo.save(item)
  log.info('[Item]<UPDATE> ' + JSON.stringify(item))
}

export const saveDetail = async (detail: Detail, item: Item) => {
  const details: Detail[] = await detailRepo.find({
    where: {
      fid: detail.fid,
      tid: detail.tid
    }
  })
  if (_.isEmpty(details)) {
    await detailRepo.save(detail)
    log.info('[DETAIL]<CREATE> ' + JSON.stringify(detail))
    vistedItem(item)
  }
}
