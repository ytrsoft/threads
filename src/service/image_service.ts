import _ from 'lodash'
import { Image } from '../entities/image.js'
import { BaseService } from './base_service.js'

export class ImageService extends BaseService<Image> {

  constructor() {
    super(Image)
  }

}
