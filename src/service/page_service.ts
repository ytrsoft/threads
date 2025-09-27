import _ from 'lodash'
import sqlite from '../sqlite/index.js'
import { Page } from '../entities/page.js'

export class PageService {

  protected repo = sqlite.getRepository(Page)

  async save(cno: string, maxpage: number): Promise<Page[]> {
    const pages: Partial<Page>[] = []
    for (let p = 1; p <= maxpage; p++) {
      const exists = await this.repo.findOne({ where: { cno, page: p } })
      if (!exists) {
        pages.push({
          cno,
          page: p,
          pages: maxpage
        })
      }
    }
    if (_.isEmpty(pages)) return []
    return this.repo.save(pages)
  }

  async query(): Promise<Page[]> {
    return this.repo.find({
      where: { visited: false }
    })
  }

  async visited(page: Page) {
    page.visited = true
    await this.repo.save(page)
  }

}
