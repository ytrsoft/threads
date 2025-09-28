import _ from 'lodash'
import { Marker } from '../entities/marker.js'
import { BaseService } from './base_service.js'

export class MarkerService extends BaseService<Marker> {
  constructor() {
    super(Marker)
  }
}
