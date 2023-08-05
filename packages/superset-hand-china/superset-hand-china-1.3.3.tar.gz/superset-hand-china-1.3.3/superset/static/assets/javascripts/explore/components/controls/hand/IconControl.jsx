import React from 'react';
import PropTypes from 'prop-types';
import {
  Label, Row, Col, FormControl, Modal, OverlayTrigger,
  Tooltip
} from 'react-bootstrap';
import { t } from '../../../../locales';
import ControlHeader from '../../ControlHeader';
require('../../../../../visualizations/hand/font-awesome.min.css');

const propTypes = {
  description: PropTypes.string,
  label: PropTypes.string,
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func,
  value: PropTypes.string.isRequired,
};

const defaultProps = {
  onChange: () => { },
};

const ICON = ['fa-adjust', 'fa-anchor', 'fa-archive', 'fa-area-chart',
  'fa-arrows', 'fa-arrows-h', 'fa-arrows-v', 'fa-asterisk',
  'fa-at', 'fa-automobile', 'fa-balance-scale', 'fa-ban',
  'fa-bank', 'fa-bar-chart', 'fa-bar-chart-o', 'fa-barcode',
  'fa-bars', 'fa-battery-0', 'fa-battery-1', 'fa-battery-2',
  'fa-battery-3', 'fa-battery-4', 'fa-battery-empty', 'fa-battery-full',
  'fa-battery-half', 'fa-battery-quarter', 'fa-battery-three-quarters', 'fa-bed',
  'fa-beer', 'fa-bell', 'fa-bell-o', 'fa-bell-slash',
  'fa-bell-slash-o', 'fa-bicycle', 'fa-binoculars', 'fa-birthday-cake',
  'fa-bolt', 'fa-bomb', 'fa-book', 'fa-bookmark',
  'fa-bookmark-o', 'fa-briefcase', 'fa-bug', 'fa-building',
  'fa-building-o', 'fa-bullhorn', 'fa-bullseye', 'fa-bus',
  'fa-cab', 'fa-calculator', 'fa-calendar', 'fa-calendar-check-o',
  'fa-calendar-minus-o', 'fa-calendar-o', 'fa-calendar-plus-o', 'fa-calendar-times-o',
  'fa-camera', 'fa-camera-retro', 'fa-car', 'fa-caret-square-o-down',
  'fa-caret-square-o-left', 'fa-caret-square-o-right', 'fa-caret-square-o-up',
  'fa-cart-arrow-down', 'fa-cart-plus', 'fa-cc', 'fa-certificate',
  'fa-check', 'fa-check-circle', 'fa-check-circle-o', 'fa-check-square',
  'fa-check-square-o', 'fa-child', 'fa-circle', 'fa-circle-o',
  'fa-circle-o-notch', 'fa-circle-thin', 'fa-clock-o', 'fa-clone',
  'fa-close', 'fa-cloud', 'fa-cloud-download', 'fa-cloud-upload',
  'fa-code', 'fa-code-fork', 'fa-coffee', 'fa-cog',
  'fa-cogs', 'fa-comment', 'fa-comment-o', 'fa-commenting',
  'fa-commenting-o', 'fa-comments', 'fa-comments-o', 'fa-compass',
  'fa-copyright', 'fa-creative-commons', 'fa-credit-card', 'fa-crop',
  'fa-crosshairs', 'fa-cube', 'fa-cubes', 'fa-cutlery',
  'fa-dashboard', 'fa-database', 'fa-desktop', 'fa-diamond',
  'fa-dot-circle-o', 'fa-download', 'fa-edit', 'fa-ellipsis-h',
  'fa-ellipsis-v', 'fa-envelope', 'fa-envelope-o', 'fa-envelope-square',
  'fa-eraser', 'fa-exchange', 'fa-exclamation', 'fa-exclamation-circle',
  'fa-exclamation-triangle', 'fa-external-link', 'fa-external-link-square', 'fa-eye',
  'fa-eye-slash', 'fa-eyedropper', 'fa-fax', 'fa-feed',
  'fa-female', 'fa-fighter-jet', 'fa-file-archive-o', 'fa-file-audio-o',
  'fa-file-code-o', 'fa-file-excel-o', 'fa-file-image-o', 'fa-file-movie-o',
  'fa-file-pdf-o', 'fa-file-photo-o', 'fa-file-picture-o', 'fa-file-powerpoint-o',
  'fa-file-sound-o', 'fa-file-video-o', 'fa-file-word-o', 'fa-file-zip-o',
  'fa-film', 'fa-filter', 'fa-fire', 'fa-fire-extinguisher',
  'fa-flag', 'fa-flag-checkered', 'fa-flag-o', 'fa-flash',
  'fa-flask', 'fa-folder', 'fa-folder-o', 'fa-folder-open',
  'fa-folder-open-o', 'fa-frown-o', 'fa-futbol-o', 'fa-gamepad',
  'fa-gavel', 'fa-gear', 'fa-gears', 'fa-gift',
  'fa-glass', 'fa-globe', 'fa-graduation-cap', 'fa-group',
  'fa-hand-grab-o', 'fa-hand-lizard-o', 'fa-hand-paper-o', 'fa-hand-peace-o',
  'fa-hand-pointer-o', 'fa-hand-rock-o', 'fa-hand-scissors-o', 'fa-hand-spock-o',
  'fa-hand-stop-o', 'fa-hdd-o', 'fa-headphones', 'fa-heart',
  'fa-heart-o', 'fa-heartbeat', 'fa-history', 'fa-home',
  'fa-hotel', 'fa-hourglass', 'fa-hourglass-1', 'fa-hourglass-2',
  'fa-hourglass-3', 'fa-hourglass-end', 'fa-hourglass-half', 'fa-hourglass-o',
  'fa-hourglass-start', 'fa-i-cursor', 'fa-image', 'fa-inbox',
  'fa-industry', 'fa-info', 'fa-info-circle', 'fa-institution',
  'fa-key', 'fa-keyboard-o', 'fa-language', 'fa-laptop',
  'fa-leaf', 'fa-legal', 'fa-lemon-o', 'fa-level-down',
  'fa-level-up', 'fa-life-bouy', 'fa-life-buoy', 'fa-life-ring',
  'fa-life-saver', 'fa-lightbulb-o', 'fa-line-chart', 'fa-location-arrow',
  'fa-lock', 'fa-magic', 'fa-magnet', 'fa-mail-forward',
  'fa-mail-reply', 'fa-mail-reply-all', 'fa-male', 'fa-map',
  'fa-map-marker', 'fa-map-o', 'fa-map-pin', 'fa-map-signs',
  'fa-meh-o', 'fa-microphone', 'fa-microphone-slash', 'fa-minus',
  'fa-minus-circle', 'fa-minus-square', 'fa-minus-square-o', 'fa-mobile',
  'fa-mobile-phone', 'fa-money', 'fa-moon-o', 'fa-mortar-board',
  'fa-motorcycle', 'fa-mouse-pointer', 'fa-music', 'fa-navicon',
  'fa-newspaper-o', 'fa-object-group', 'fa-object-ungroup', 'fa-paint-brush',
  'fa-paper-plane', 'fa-paper-plane-o', 'fa-paw', 'fa-pencil',
  'fa-pencil-square', 'fa-pencil-square-o', 'fa-phone', 'fa-phone-square',
  'fa-photo', 'fa-picture-o', 'fa-pie-chart', 'fa-plane',
  'fa-plug', 'fa-plus', 'fa-plus-circle', 'fa-plus-square',
  'fa-plus-square-o', 'fa-power-off', 'fa-print', 'fa-puzzle-piece',
  'fa-qrcode', 'fa-question', 'fa-question-circle', 'fa-quote-left',
  'fa-quote-right', 'fa-random', 'fa-recycle', 'fa-refresh',
  'fa-registered', 'fa-remove', 'fa-reorder', 'fa-reply',
  'fa-reply-all', 'fa-retweet', 'fa-road', 'fa-rocket',
  'fa-rss', 'fa-rss-square', 'fa-search', 'fa-search-minus',
  'fa-search-plus', 'fa-send', 'fa-send-o', 'fa-server',
  'fa-share', 'fa-share-alt', 'fa-share-alt-square', 'fa-share-square',
  'fa-share-square-o', 'fa-shield', 'fa-ship', 'fa-shopping-cart',
  'fa-sign-in', 'fa-sign-out', 'fa-signal', 'fa-sitemap',
  'fa-sliders', 'fa-smile-o', 'fa-soccer-ball-o', 'fa-sort',
  'fa-sort-alpha-asc', 'fa-sort-alpha-desc', 'fa-sort-amount-asc', 'fa-sort-amount-desc',
  'fa-sort-asc', 'fa-sort-desc', 'fa-sort-down', 'fa-sort-numeric-asc',
  'fa-sort-numeric-desc', 'fa-sort-up', 'fa-space-shuttle', 'fa-spinner',
  'fa-spoon', 'fa-square', 'fa-square-o', 'fa-star',
  'fa-star-half', 'fa-star-half-empty', 'fa-star-half-full', 'fa-star-half-o',
  'fa-star-o', 'fa-sticky-note', 'fa-sticky-note-o', 'fa-street-view',
  'fa-suitcase', 'fa-sun-o', 'fa-support', 'fa-tablet',
  'fa-tachometer', 'fa-tag', 'fa-tags', 'fa-tasks',
  'fa-taxi', 'fa-television', 'fa-terminal', 'fa-thumb-tack',
  'fa-thumbs-down', 'fa-thumbs-o-down', 'fa-thumbs-o-up', 'fa-thumbs-up',
  'fa-ticket', 'fa-times', 'fa-times-circle', 'fa-times-circle-o',
  'fa-tint', 'fa-toggle-down', 'fa-toggle-left', 'fa-toggle-off',
  'fa-toggle-on', 'fa-toggle-right', 'fa-toggle-up', 'fa-trademark',
  'fa-trash', 'fa-trash-o', 'fa-tree', 'fa-trophy',
  'fa-truck', 'fa-tty', 'fa-tv', 'fa-umbrella',
  'fa-university', 'fa-unlock', 'fa-unlock-alt', 'fa-unsorted',
  'fa-upload', 'fa-user', 'fa-user-plus', 'fa-user-secret',
  'fa-user-times', 'fa-users', 'fa-video-camera', 'fa-volume-down',
  'fa-volume-off', 'fa-volume-up', 'fa-warning', 'fa-wheelchair',
  'fa-wifi', 'fa-wrench'];
const ICONNAME = [
  'adjust',
  'anchor', 'archive', 'area-chart', 'arrows',
  'arrows-h', 'arrows-v', 'asterisk', 'at',
  'automobile', 'balance-scale', 'ban', 'bank',
  'bar-chart', 'bar-chart-o', 'barcode', 'bars',
  'battery-0', 'battery-1', 'battery-2', 'battery-3',
  'battery-4', 'battery-empty', 'battery-full', 'battery-half',
  'battery-quarter', 'battery-three-quarters', 'bed', 'beer',
  'bell', 'bell-o', 'bell-slash', 'bell-slash-o',
  'bicycle', 'binoculars', 'birthday-cake', 'bolt',
  'bomb', 'book', 'bookmark', 'bookmark-o',
  'briefcase', 'bug', 'building', 'building-o',
  'bullhorn', 'bullseye', 'bus', 'cab',
  'calculator', 'calendar', 'calendar-check-o', 'calendar-minus-o',
  'calendar-o', 'calendar-plus-o', 'calendar-times-o', 'camera',
  'camera-retro', 'car', 'caret-square-o-down', 'caret-square-o-left',
  'caret-square-o-right', 'caret-square-o-up', 'cart-arrow-down', 'cart-plus',
  'cc', 'certificate', 'check', 'check-circle',
  'check-circle-o', 'check-square', 'check-square-o', 'child',
  'circle', 'circle-o', 'circle-o-notch', 'circle-thin',
  'clock-o', 'clone', 'close', 'cloud',
  'cloud-download', 'cloud-upload', 'code', 'code-fork',
  'coffee', 'cog', 'cogs', 'comment',
  'comment-o', 'commenting', 'commenting-o', 'comments',
  'comments-o', 'compass', 'copyright', 'creative-commons',
  'credit-card', 'crop', 'crosshairs', 'cube',
  'cubes', 'cutlery', 'dashboard', 'database',
  'desktop', 'diamond', 'dot-circle-o', 'download',
  'edit', 'ellipsis-h', 'ellipsis-v', 'envelope',
  'envelope-o', 'envelope-square', 'eraser', 'exchange',
  'exclamation', 'exclamation-circle', 'exclamation-triangle', 'external-link',
  'external-link-square', 'eye', 'eye-slash', 'eyedropper',
  'fax', 'feed', 'female', 'fighter-jet',
  'file-archive-o', 'file-audio-o', 'file-code-o', 'file-excel-o',
  'file-image-o', 'file-movie-o', 'file-pdf-o', 'file-photo-o',
  'file-picture-o', 'file-powerpoint-o', 'file-sound-o', 'file-video-o',
  'file-word-o', 'file-zip-o', 'film', 'filter',
  'fire', 'fire-extinguisher', 'flag', 'flag-checkered',
  'flag-o', 'flash', 'flask', 'folder',
  'folder-o', 'folder-open', 'folder-open-o', 'frown-o',
  'futbol-o', 'gamepad', 'gavel', 'gear',
  'gears', 'gift', 'glass', 'globe',
  'graduation-cap', 'group', 'hand-grab-o', 'hand-lizard-o',
  'hand-paper-o', 'hand-peace-o', 'hand-pointer-o', 'hand-rock-o',
  'hand-scissors-o', 'hand-spock-o', 'hand-stop-o', 'hdd-o',
  'headphones', 'heart', 'heart-o', 'heartbeat',
  'history', 'home', 'hotel', 'hourglass',
  'hourglass-1', 'hourglass-2', 'hourglass-3', 'hourglass-end',
  'hourglass-half', 'hourglass-o', 'hourglass-start', 'i-cursor',
  'image', 'inbox', 'industry', 'info',
  'info-circle', 'institution', 'key', 'keyboard-o',
  'language', 'laptop', 'leaf', 'legal',
  'lemon-o', 'level-down', 'level-up', 'life-bouy',
  'life-buoy', 'life-ring', 'life-saver', 'lightbulb-o',
  'line-chart', 'location-arrow', 'lock', 'magic',
  'magnet', 'mail-forward', 'mail-reply', 'mail-reply-all',
  'male', 'map', 'map-marker', 'map-o',
  'map-pin', 'map-signs', 'meh-o', 'microphone',
  'microphone-slash', 'minus', 'minus-circle', 'minus-square',
  'minus-square-o', 'mobile', 'mobile-phone', 'money',
  'moon-o', 'mortar-board', 'motorcycle', 'mouse-pointer',
  'music', 'navicon', 'newspaper-o', 'object-group',
  'object-ungroup', 'paint-brush', 'paper-plane', 'paper-plane-o',
  'paw', 'pencil', 'pencil-square', 'pencil-square-o',
  'phone', 'phone-square', 'photo', 'picture-o',
  'pie-chart', 'plane', 'plug', 'plus',
  'plus-circle', 'plus-square', 'plus-square-o', 'power-off',
  'print', 'puzzle-piece', 'qrcode', 'question',
  'question-circle', 'quote-left', 'quote-right', 'random',
  'recycle', 'refresh', 'registered', 'remove',
  'reorder', 'reply', 'reply-all', 'retweet',
  'road', 'rocket', 'rss', 'rss-square',
  'search', 'search-minus', 'search-plus', 'send',
  'send-o', 'server', 'share', 'share-alt',
  'share-alt-square', 'share-square', 'share-square-o', 'shield',
  'ship', 'shopping-cart', 'sign-in', 'sign-out',
  'signal', 'sitemap', 'sliders', 'smile-o',
  'soccer-ball-o', 'sort', 'sort-alpha-asc', 'sort-alpha-desc',
  'sort-amount-asc', 'sort-amount-desc', 'sort-asc', 'sort-desc',
  'sort-down', 'sort-numeric-asc', 'sort-numeric-desc', 'sort-up',
  'space-shuttle', 'spinner', 'spoon', 'square',
  'square-o', 'star', 'star-half', 'star-half-empty',
  'star-half-full', 'star-half-o', 'star-o', 'sticky-note',
  'sticky-note-o', 'street-view', 'suitcase', 'sun-o',
  'support', 'tablet', 'tachometer', 'tag',
  'tags', 'tasks', 'taxi', 'television',
  'terminal', 'thumb-tack', 'thumbs-down', 'thumbs-o-down',
  'thumbs-o-up', 'thumbs-up', 'ticket', 'times',
  'times-circle', 'times-circle-o', 'tint', 'toggle-down',
  'toggle-left', 'toggle-off', 'toggle-on', 'toggle-right',
  'toggle-up', 'trademark', 'trash', 'trash-o',
  'tree', 'trophy', 'truck', 'tty',
  'tv', 'umbrella', 'university', 'unlock',
  'unlock-alt', 'unsorted', 'upload', 'user',
  'user-plus', 'user-secret', 'user-times', 'users',
  'video-camera', 'volume-down', 'volume-off', 'volume-up',
  'warning', 'wheelchair', 'wifi', 'wrench'];

export default class IconControl extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      showModal: false,
      filter: '',
    };
    this.toggleModal = this.toggleModal.bind(this);
    this.changeSearch = this.changeSearch.bind(this);
    this.setSearchRef = this.setSearchRef.bind(this);
    this.focusSearch = this.focusSearch.bind(this);
  }
  onChange(vizType) {
    this.props.onChange(vizType);
    this.setState({ showModal: false });
  }
  setSearchRef(searchRef) {
    this.searchRef = searchRef;
  }
  toggleModal() {
    this.setState({ showModal: !this.state.showModal });
  }
  changeSearch(event) {
    this.setState({ filter: event.target.value });
  }
  focusSearch() {
    if (this.searchRef) {
      this.searchRef.focus();
    }
  }

  render() {
    const filter = this.state.filter;
    const imgPerRow = 4;
    const rows = [];
    var count = 0;

    for (let i = 0; i < ICON.length; i += imgPerRow) {
      rows.push(
        <Row key={`row-${i}`}>
          <Col style={{ cursor: 'pointer' }} md={3} key={`grid-col-${count * imgPerRow}`}>
            <div
              className={`big-number ${ICON[count * imgPerRow] === this.props.value ? 'selected' : ''}`}
              onClick={this.onChange.bind(this, ICON[count * imgPerRow])}
            >
              <i className={`fa ${ICON[count * imgPerRow]}`}></i> {ICONNAME[count * imgPerRow]}
            </div>
          </Col>
          <Col style={{ cursor: 'pointer' }} md={3} key={`grid-col-${count * imgPerRow + 1}`}>
            <div
              className={`big-number ${ICON[count * imgPerRow + 1] === this.props.value ? 'selected' : ''}`}
              onClick={this.onChange.bind(this, ICON[count * imgPerRow + 1])}
            >
              <i className={`fa ${ICON[count * imgPerRow + 1]}`}></i> {ICONNAME[count * imgPerRow + 1]}
            </div>
          </Col>
          <Col style={{ cursor: 'pointer' }} md={3} key={`grid-col-${count * imgPerRow + 2}`}>
            <div
              className={`big-number ${ICON[count * imgPerRow + 2] === this.props.value ? 'selected' : ''}`}
              onClick={this.onChange.bind(this, ICON[count * imgPerRow + 2])}
            >
              <i className={`fa ${ICON[count * imgPerRow + 2]}`}></i> {ICONNAME[count * imgPerRow + 2]}
            </div>
          </Col>
          <Col style={{ cursor: 'pointer' }} md={3} key={`grid-col-${count * imgPerRow + 3}`}>
            <div
              className={`big-number ${ICON[count * imgPerRow + 3] === this.props.value ? 'selected' : ''}`}
              onClick={this.onChange.bind(this, ICON[count * imgPerRow + 3])}
            >
              <i className={`fa ${ICON[count * imgPerRow + 3]}`}></i> {ICONNAME[count * imgPerRow + 3]}
            </div>
          </Col>
        </Row>

      );
      count++;
    }


    return (
      <div>
        <ControlHeader
          {...this.props}
        />
        <OverlayTrigger
          placement="right"
          overlay={
            <Tooltip id={'error-tooltip'}>{t('Click to change visualization type')}</Tooltip>
          }
        >
          <Label onClick={this.toggleModal} style={{ cursor: 'pointer' }}>
            <i className={'fa ' + this.props.value}></i>{this.props.value.substring(3, this.props.value.length)}
          </Label>
        </OverlayTrigger>
        <Modal
          show={this.state.showModal}
          onHide={this.toggleModal}
          onEnter={this.focusSearch}
          onExit={this.setSearchRef}
          bsSize="lg"
        >
          <Modal.Header closeButton>
            <Modal.Title>{t('Select icon ')}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {rows}
          </Modal.Body>
        </Modal>
      </div>);
  }
}

IconControl.propTypes = propTypes;
IconControl.defaultProps = defaultProps;
