import { Page } from 'playwright'
import { PlaywrightCrawler } from 'crawlee'
import { BASE_URL } from '../utils/index.js'
import { queryItems, saveDetail } from '../service/data_service.js'
import { Item } from '../entities/item.js'
import { Detail } from '../entities/detail.js'

const detailRoute = async(item: Item, page: Page): Promise<Detail> => {
  const name = await page.$eval(
    '.card-thread .media-body h4',
    el => el.textContent?.trim() || ''
  ).catch(() => '')
  const desc = await page.$eval(
    '.card-body blockquote span',
    el => el.textContent?.trim() || ''
  ).catch(() => '')
  const imgs = await page.$$eval(
    '.card-thread img.img-fluid',
    els => els.map(el => (el as HTMLImageElement).src)
  ).catch(() => [])
  const cells = await page.$$eval(
    '.card-body tbody tr',
    rows => {
      const data: string[]= []
      for (const row of rows) {
        const tds = row.querySelectorAll('td')
        tds.forEach((item) => {
          data.push(item.textContent?.trim() || '')
        })
      }
      return data
    }
  ).catch(() => Array(8).fill(''))

  return {
    fid: item.fid,
    tid: item.tid,
    name,
    desc,
    imgs: JSON.stringify(imgs),
    region: cells[0],
    age: cells[1],
    beauty: cells[2],
    price: cells[3],
    service: cells[4],
    wechat: cells[5],
    qq: cells[6],
    phone: cells[7]
  } as Detail
}

export default async function() {
  const inst = new PlaywrightCrawler({
    async requestHandler({ request, page }) {
      const item = request.userData.item as Item
      const detail = await detailRoute(item, page)
      await saveDetail(detail, item)
    }
  })

  const items = await queryItems()

  const requests = items.map((item) => {
    return {
      userData: {
        item
      },
      url: `${BASE_URL}/thread-${item.tid}.htm`
    }
  })

  await inst.addRequests(requests)

  await inst.run()
}
