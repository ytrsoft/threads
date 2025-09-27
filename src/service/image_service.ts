import _ from 'lodash'
import sqlite from '../sqlite/index.js'
import { Image } from '../entities/image.js'

export class ImageService {

  protected repo = sqlite.getRepository(Image)

  async save(images: Partial<Image>[]): Promise<Image[]> {
    return this.repo.save(images)
  }

  async query(): Promise<Image[]> {
    return this.repo.find({where: { visited: false}})
  }

  async visited(image: Image) {
    image.visited = true
    await this.repo.save(image)
  }

}
