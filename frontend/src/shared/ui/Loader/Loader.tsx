import cx from 'classnames'

interface ILoader {
  size?: "small" | "medium" | "large"
}

export const Loader: React.FC<ILoader> = ({size = "medium"}) => {

  return (
      <span className={cx("border-[#FF3D00] border-b-transparent inline-block animate-rotation rounded-[50%] ", {
        "w-6 h-6 border-[3px]": size === "small",
        "w-8 h-8 border-[5px]": size === "medium",
        "w-12 h-12 border-[6px]": size === "large",
      })}></span>
  )
}