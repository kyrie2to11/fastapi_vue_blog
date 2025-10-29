import { mount } from '@vue/test-utils';
import Kancolle from './Kancolle.vue';

describe('Kancolle.vue', () => {
  it('renders the companion container and character image', () => {
    const wrapper = mount(Kancolle);
    expect(wrapper.find('.kancolle-container').exists()).toBe(true);
    expect(wrapper.find('.kancolle-character').exists()).toBe(true);
  });

  it('displays greeting text and has "Say Hi" button', () => {
    const wrapper = mount(Kancolle);
    expect(wrapper.find('.kancolle-text p').text()).toContain('Hello! I\'m your Kancolle companion~');
    expect(wrapper.find('button').text()).toContain('Say Hi');
  });

  it('triggers alert when "Say Hi" button is clicked', async () => {
    window.alert = jest.fn();
    const wrapper = mount(Kancolle);
    await wrapper.find('button').trigger('click');
    expect(window.alert).toHaveBeenCalledWith('Nice to meet you!');
  });
});