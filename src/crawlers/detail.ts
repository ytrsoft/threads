import { Page } from 'playwright'
import { PlaywrightCrawler } from 'crawlee'
import { BASE_URL } from '../utils/index.js'

import { PostService } from '../service/post_service.js'
import { MarkerService } from '../service/maker_service.js'
import { ImageService } from '../service/image_service.js'
import { Marker } from '../entities/marker.js'
import { Post } from '../entities/post.js'
import { Image } from '../entities/image.js'
import { Entity } from '../service/base_service.js'

const postService = new PostService()
const markService = new MarkerService()
const imageService = new ImageService()

interface Detail {
  images: Entity<Image>,
  post: Entity<Post>
}

const detailRoute = async(marker: Marker, page: Page): Promise<Detail> => {
  const title = await page.$eval(
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
  const images = imgs.map((src) => {
    return {
      src,
      pid: marker.pid
    }
  })
  const post = {
    title,
    desc,
    id: marker.pid,
    cid: marker.cid,
    region: cells[0],
    age: cells[1],
    score: cells[2],
    price: cells[3],
    service: cells[4],
    wechat: cells[5],
    qq: cells[6],
    phone: cells[7]
  }
  return { images, post }
}

export default async function() {
  const inst = new PlaywrightCrawler({
    async requestHandler({ request, page }) {
      const { marker } = request.userData.entity
      const { images, post } = await detailRoute(
        marker, page
      )
      postService.save(post)
      imageService.save(images)
      markService.visited(marker)
    }
  })

  const markers = await markService.queryForList()

  const requests = markers.map((marker) => {
    return {
      userData: {
        entity: {
          marker
        }
      },
      url: `${BASE_URL}/thread-${marker.pid}.htm`
    }
  })

  await inst.addRequests(requests)

  await inst.run()
}
