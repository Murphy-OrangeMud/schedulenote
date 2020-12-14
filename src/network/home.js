import { request } from './request'

export function getHomeMultidata () {
  return request({
    url: '/course/filelist'
  })
}

export function getHomeGoods (type, page) {
  return request({
    url: '/home/data',
    params: {
      type,
      page
    }
  })
}
