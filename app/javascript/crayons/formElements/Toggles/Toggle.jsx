// @specre 01KJXZHA0MNZG1M31EXQKE9VX8
import { h } from 'preact';

export const Toggle = ({ ...otherProps }) => {
  return <input type="checkbox" className="c-toggle" {...otherProps} />;
};

Toggle.displayName = 'Toggle';
