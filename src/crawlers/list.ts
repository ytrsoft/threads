import { Page } from 'playwright'
import { PlaywrightCrawler } from 'crawlee'
import { BASE_URL } from '../utils/index.js'
import { queryFlag, saveItems } from '../service/data_service.js'
import { Item } from '../entities/item.js'
import { Flag } from '../entities/flag.js'

const itemRoute = async(fid: string, page: Page): Promise<Item[]> => {
  return await page.$$eval('.list-unstyled.threadlist li', (list) => {
    const items: Item[] = []
    list.forEach((li) => {
      const tid = li.getAttribute('data-tid') as string
      items.push({ tid, fid } as Item)
    })
    return items
  })
}

export default async function() {
  const inst = new PlaywrightCrawler({
    async requestHandler({ request, page }) {
      const flag = request.userData.flag as Flag
      const items = await itemRoute(
        flag.fid as string, page
      )
      await saveItems(items, flag)
    }
  })

  const flags = await queryFlag()

  const requests = flags.map((flag) => {
    return {
      userData: {
        flag
      },
      url: `${BASE_URL}/forum-${flag.fid}-${flag.page}.htm?orderby=lastpid&digest=0`
    }
  })

  await inst.addRequests(requests)

  await inst.run()
}
