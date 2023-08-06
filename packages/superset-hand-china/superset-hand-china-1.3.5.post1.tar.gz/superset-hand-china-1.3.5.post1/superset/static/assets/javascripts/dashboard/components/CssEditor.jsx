import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';

import AceEditor from 'react-ace';
import 'brace/mode/css';
import 'brace/theme/github';

import ModalTrigger from '../../components/ModalTrigger';
import { t } from '../../locales';

const propTypes = {
  initialCss: PropTypes.string,
  triggerNode: PropTypes.node.isRequired,
  onChange: PropTypes.func,
  templates: PropTypes.array,
  themes: PropTypes.array,
  theme: PropTypes.string,
  sliceResizeAble: PropTypes.array,
  refreshAble: PropTypes.bool,
};

const defaultProps = {
  initialCss: '',
  onChange: () => {},
  templates: [],
  theme: '',
  refreshAble: true,
};

class CssEditor extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      css: props.initialCss,
      cssTemplateOptions: [],
      theme: props.theme,
      refreshAble: props.refreshAble,
    };
  }
  componentWillMount() {
    this.updateDom();
  }
  changeCss(css) {
    this.setState({ css }, this.updateDom);
    this.props.onChange(css, 'css');
  }
  updateDom() {
    const css = this.state.css;
    const className = 'CssEditor-css';
    const head = document.head || document.getElementsByTagName('head')[0];
    let style = document.querySelector('.' + className);

    if (!style) {
      style = document.createElement('style');
      style.className = className;
      style.type = 'text/css';
      head.appendChild(style);
    }
    if (style.styleSheet) {
      style.styleSheet.cssText = css;
    } else {
      style.innerHTML = css;
    }
  }
  changeCssTemplate(opt) {
    this.changeCss(opt.css);
  }

  changeTheme(dashboard, opt) {
    this.setState({ theme: opt.value });
    dashboard.slices.forEach((data) => {
      dashboard.getSlice(data.slice_id).render(true, opt.value);
    });
    this.props.onChange(opt.value, 'theme');
  }

  changeResize(dashboard, opt) {
    this.setState({ refreshAble: opt.value });
    dashboard.refreshAble = opt.value;
    this.props.onChange(opt.value, 'refresh')
  }

  renderTemplateSelector() {
    if (this.props.templates) {
      return (
        <div style={{ zIndex: 10 }}>
          <h5>{t('Load a template')}</h5>
          <Select
            options={this.props.templates}
            placeholder={t('Load a CSS template')}
            onChange={this.changeCssTemplate.bind(this)}
            noResultsText={t('No Results Found')}
          />
        </div>
      );
    }
    return null;
  }
  renderThemeSelector(dashboard) {
    if (this.props.themes) {
      return (
        <div style={{ zIndex: 10 }}>
          <h5>{t('Load a Theme')}</h5>
          <Select
            options={this.props.themes.map((o) => ({ value: o, label: o }))}
            placeholder={t('Choose Slice Theme')}
            onChange={this.changeTheme.bind(this, dashboard)}
            value={this.state.theme}
            noResultsText={t('No Results Found')}
            />
        </div>
      );
    }
    return null;
  }

  renderResizeSelector(dashboard) {
    if (this.props.sliceResizeAble) {
      const sliceResizeVal = [];
      for (let i = 0; i < this.props.sliceResizeAble.length; i++) {
        if (this.props.sliceResizeAble[i]) {
          sliceResizeVal.push({ value: this.props.sliceResizeAble[i], label: t('True') });
        } else if(!this.props.sliceResizeAble[i]) {
          sliceResizeVal.push({ value: this.props.sliceResizeAble[i], label: t('False') });
        } else {
          sliceResizeVal.push({ value: this.props.sliceResizeAble[i], label: this.props.sliceResizeAble[i] });
        }
      }
      return (
        <div style={{ zIndex: 10 }}>
          <h5>{t('The window changes the size to refresh the slice')}</h5>
          <Select
            // options={this.props.sliceResizeAble.map((o) => ({ value: o, label: o }))}
            options={sliceResizeVal}
            placeholder={t('The window changes the size to refresh the slice')}
            onChange={this.changeResize.bind(this, dashboard)}
            value={this.state.refreshAble}
            noResultsText={t('No Results Found')}
            />
        </div>
      );
    }
    return null;
  }
  render() {
    return (
      <ModalTrigger
        triggerNode={this.props.triggerNode}
        modalTitle={t('CSS')}
        isButton
        modalBody={
          <div>
            {this.renderResizeSelector(this.props.dashboard)}
            {this.renderTemplateSelector()}
            {this.renderThemeSelector(this.props.dashboard)}
            <div style={{ zIndex: 1 }}>
              <h5>{t('Live CSS Editor')}</h5>
              <div style={{ border: 'solid 1px grey' }}>
                <AceEditor
                  mode="css"
                  theme="github"
                  minLines={8}
                  maxLines={30}
                  onChange={this.changeCss.bind(this)}
                  height="200px"
                  width="100%"
                  editorProps={{ $blockScrolling: true }}
                  enableLiveAutocompletion
                  value={this.state.css || ''}
                />
              </div>
            </div>
          </div>
        }
      />
    );
  }
}
CssEditor.propTypes = propTypes;
CssEditor.defaultProps = defaultProps;

export default CssEditor;
